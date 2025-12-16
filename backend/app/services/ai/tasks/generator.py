"""app.services.ai.tasks.generator
为教师向导提供题面与测评集生成实现。

实现策略：使用 `app.services.ai.client.call_llm` 发送 prompt（由 `prompts.build_feedback_prompt`/自定义 prompt 构建）
返回结构化数据：
- generate_problem(description) -> { 'readme': str, 'solution': str }
- generate_tests(readme, solution, count=20) -> { 'tests': [ { 'input': str, 'output': str }, ... ] }

注意：本实现尽量保持简单、可用性优先；实际部署请根据 LLM 返回格式调整解析逻辑并添加更严格的安全/长度限制。
"""

from typing import List, Dict, Any
import json
import asyncio
import argparse

from app.services.ai.client import call_llm, AIClientError
from app.services.ai.prompts import build_problem_generation_prompt, build_tests_generation_prompt


async def generate_problem(description: str) -> Dict[str, str]:
	"""根据教师的简要描述生成 README（题面）与 solution（参考答案）。

	返回：{ 'readme': ..., 'solution': ... }
	"""
	if not description or not description.strip():
		raise ValueError('description 不能为空')

	messages = build_problem_generation_prompt(description)
	try:
		text = await call_llm(messages, temperature=0.2)
	except AIClientError as e:
		raise

	# 尝试解析 JSON 字符串
	try:
		jtxt = extract_json(text)
		data = json.loads(jtxt)
		readme = data.get('readme', '')
		solution = data.get('solution', '')

		# 规范 solution：仅保留 python 代码块。如果 LLM 返回裸代码，则将其包装成 ```python 代码块；
		# 如果包含多个代码块，优先提取第一个 python 代码块。
		if isinstance(solution, str):
			sol = solution.strip()
			# 尝试提取 ```python ``` 之间的代码
			import re
			m = re.search(r'```\s*python\s*([\s\S]*?)```', sol, re.IGNORECASE)
			if m:
				code = m.group(1).strip()
				solution = '```python\n' + code + '\n```'
			else:
				# 如果没有代码块，尝试提取任意 ``` ``` 中的代码
				m2 = re.search(r'```([\s\S]*?)```', sol)
				if m2:
					code = m2.group(1).strip()
					solution = '```python\n' + code + '\n```'
				else:
					# 认为整个内容即为代码，将其包装
					solution = '```python\n' + sol + '\n```'

		return {'readme': readme, 'solution': solution}
	except Exception:
		# 回退：将 LLM 完整文本作为 readme，solution 为空
		return {'readme': text, 'solution': ''}


async def generate_tests(readme: str, solution: str, count: int = 20) -> Dict[str, List[Dict[str, str]]]:
	"""根据题面与参考答案生成若干测试用例。

	返回：{ 'tests': [ {'input': '...', 'output': '...'}, ... ] }
	"""
	if not solution or not solution.strip():
		raise ValueError('solution 不能为空以生成测试用例')

	messages = build_tests_generation_prompt(readme, solution, count)
	try:
		text = await call_llm(messages, temperature=0.1)
	except AIClientError:
		raise

	try:
		jtxt = extract_json(text)
		data = json.loads(jtxt)
		tests = data.get('tests') or []
		out = []
		for t in tests[:count]:
			if isinstance(t, dict):
				inp = t.get('input', '')
				outp = t.get('output', '')
				out.append({'input': str(inp), 'output': str(outp)})
		while len(out) < count:
			out.append({'input': '', 'output': ''})
		return {'tests': out}
	except Exception:
		parsed = parse_tests_from_text(text, count)
		return {'tests': parsed}


def extract_json(text: str) -> str:
	"""尝试从 LLM 返回中提取第一个 JSON 对象子串。"""
	if not text:
		return '{}'
	s = text.strip()
	first = s.find('{')
	last = s.rfind('}')
	if first >= 0 and last > first:
		return s[first:last+1]
	return s


def parse_tests_from_text(text: str, count: int) -> List[Dict[str, str]]:
	"""从自由文本尝试解析测试用例，格式化为列表。简单实现：按行查找包含 '->' 或 ':' 的对。"""
	lines = [l.strip() for l in text.splitlines() if l.strip()]
	out = []
	for line in lines:
		if '->' in line:
			parts = line.split('->', 1)
		elif ':' in line:
			parts = line.split(':', 1)
		else:
			continue
		inp = parts[0].strip()
		outp = parts[1].strip()
		out.append({'input': inp, 'output': outp})
		if len(out) >= count:
			break
	while len(out) < count:
		out.append({'input': '', 'output': ''})
	return out


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='AI Problem/Tests generator (debug CLI)')
	parser.add_argument('--description', '-d', help='简要题目描述，用于生成 README & solution')
	parser.add_argument('--readme', help='已有 README，用于生成测试用例')
	parser.add_argument('--solution', help='已有 solution，用于生成测试用例')
	parser.add_argument('--tests', type=int, default=20, help='生成测试用例数量')
	args = parser.parse_args()

	async def main():
		if args.description:
			res = await generate_problem(args.description)
			print('--- README.md ---')
			print(res.get('readme',''))
			print('--- solution.md ---')
			print(res.get('solution',''))
		elif args.readme and args.solution:
			res = await generate_tests(args.readme, args.solution, args.tests)
			print(json.dumps(res, ensure_ascii=False, indent=2))
		else:
			print('请提供 --description 或 --readme 和 --solution')

	asyncio.run(main())
