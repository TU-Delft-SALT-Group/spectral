import { expect, test } from 'vitest';
import { deepEqual } from './utils';

test('deepEquals primitives', () => {
	expect(deepEqual(false, false)).toBe(true);
	expect(deepEqual(1, 1)).toBe(true);
	expect(deepEqual('hello', 'hello')).toBe(true);
	expect(deepEqual(undefined, undefined)).toBe(true);
	expect(deepEqual(null, null)).toBe(true);
	expect(deepEqual(BigInt(20), BigInt(20))).toBe(true);

	expect(deepEqual(Symbol('diff'), Symbol('diff'))).toBe(false);
	expect(deepEqual(Symbol('diff'), Symbol('yooo'))).toBe(false);
	expect(deepEqual(false, true)).toBe(false);
	expect(deepEqual(1, 5)).toBe(false);
	expect(deepEqual('hello', 'hello world')).toBe(false);
	expect(deepEqual(null, undefined)).toBe(false);
	expect(deepEqual(BigInt(5), BigInt(69))).toBe(false);
	expect(
		deepEqual(
			() => 20,
			() => 20
		)
	).toBe(false);

	const func = () => 20;
	const symbol = Symbol('hello');
	expect(deepEqual(func, func)).toBe(true);
	expect(deepEqual(symbol, symbol)).toBe(true);
});

test('deepEquals object', () => {
	expect(
		deepEqual(
			{
				hello: 'world'
			},
			{
				hello: 'world'
			}
		)
	).toBe(true);

	expect(
		deepEqual(
			{
				hello: 'world',
				more: 'attributes on first'
			},
			{
				hello: 'world'
			}
		)
	).toBe(false);

	expect(
		deepEqual(
			{
				hello: 'world'
			},
			{
				hello: 'world',
				more: 'attributes on second'
			}
		)
	).toBe(false);
});

test('deepEquals exotic objects', () => {
	expect(deepEqual([1, 2, 3], [1, 2, 3])).toBe(true);
	expect(deepEqual(new Date(), new Date())).toBe(true);

	expect(deepEqual([1, 2, 3, 4], [1, 2, 3])).toBe(false);
	expect(deepEqual([1, 2, 3], [1, 2, 3, 4])).toBe(false);
	expect(deepEqual([1, 3, 3], [1, 2, 3])).toBe(false);
	expect(deepEqual(new Date(90, 4), new Date(98))).toBe(false);
});
