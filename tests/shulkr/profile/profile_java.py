from timeit import timeit

from shulkr.java import get_renamed_variables


def wrap_in_class(code: str) -> str:
	return """package foo;

	class Foo {
		public static void main(String[] args) {
			%s
		}
	}
	""" % code


def profile_get_renamed_variables():
	SAMPLES = [
		('int x = 0;', 'int x = 0;'),
		('int x = 0;', 'int y = 0;'),
		('int x, y, z;', 'int a, b, c;'),
		('int x; int y; int z;', 'int a; int b; int c;'),
		(
			'if (true) { int x = 0; } else { int x = 0; }',
			'if (true) { int x = 0; } else { int x = 0; }'
		),
		(
			'; '.join([f'int x{i}' for i in range(100)]) + ';',
			'; '.join([f'int x{i}' for i in range(100)]) + ';'
		),
		(
			'; '.join([f'int x{i}' for i in range(100)]) + ';',
			'; '.join([f'int y{i}' for i in range(100)]) + ';'
		)
	]

	total_time = 0.0

	for before, after in SAMPLES:
		print('---------------')
		print(before, end='\n')
		print(after, end='\n')
		before_wrapped = wrap_in_class(before)
		after_wrapped = wrap_in_class(after)
		duration = timeit(
			lambda: get_renamed_variables(before_wrapped, after_wrapped),
			number=100
		)
		total_time += duration
		print(f'{duration}s', end='\n\n')

	print('---------------')
	print(f'{total_time}s')
