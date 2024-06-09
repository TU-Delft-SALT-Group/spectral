import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { cubicOut } from 'svelte/easing';
import type { TransitionConfig } from 'svelte/transition';

export function cn(...inputs: ClassValue[]) {
	return twMerge(clsx(inputs));
}

type FlyAndScaleParams = {
	y?: number;
	x?: number;
	start?: number;
	duration?: number;
};

export const flyAndScale = (
	node: Element,
	params: FlyAndScaleParams = { y: -8, x: 0, start: 0.95, duration: 150 }
): TransitionConfig => {
	const style = getComputedStyle(node);
	const transform = style.transform === 'none' ? '' : style.transform;

	const scaleConversion = (valueA: number, scaleA: [number, number], scaleB: [number, number]) => {
		const [minA, maxA] = scaleA;
		const [minB, maxB] = scaleB;

		const percentage = (valueA - minA) / (maxA - minA);
		const valueB = percentage * (maxB - minB) + minB;

		return valueB;
	};

	const styleToString = (style: Record<string, number | string | undefined>): string => {
		return Object.keys(style).reduce((str, key) => {
			if (style[key] === undefined) return str;
			return str + `${key}:${style[key]};`;
		}, '');
	};

	return {
		duration: params.duration ?? 200,
		delay: 0,
		css: (t) => {
			const y = scaleConversion(t, [0, 1], [params.y ?? 5, 0]);
			const x = scaleConversion(t, [0, 1], [params.x ?? 0, 0]);
			const scale = scaleConversion(t, [0, 1], [params.start ?? 0.95, 1]);

			return styleToString({
				transform: `${transform} translate3d(${x}px, ${y}px, 0) scale(${scale})`,
				opacity: t
			});
		},
		easing: cubicOut
	};
};

/**
 * Unwrap a value that is possibly null or undefined
 */
export function unwrap<T>(
	value: T | null | undefined,
	message = 'Tried to unwrap a null value'
): T {
	if (value === null || value === undefined) {
		throw new Error(message);
	}

	return value;
}

export function todo(message: string = 'Not implemented'): never {
	throw new Error(message);
}

/**
 * Utility function to mark variables as used
 *
 * Mainly useful inside svelte, since I'm not aware of a way to tell it to not show warnings for unused variables,
 * which is sometimes necessary for a component to adhere to an interface
 */
/* eslint-disable-next-line @typescript-eslint/no-unused-vars */
export function used(..._args: unknown[]) {}

/**
 * Utility function to compare the eqality of two objects
 */
export function deepEqual(x: unknown, y: unknown): boolean {
	const tx = typeof x;
	const ty = typeof y;

	if (tx !== ty) {
		return false;
	}

	if (tx !== 'object' || x === undefined || y === undefined || x === null || y === null) {
		return x === y;
	}

	// Apparently dates are always the same or somwthing
	if (x instanceof Date && y instanceof Date) {
		return x.getTime() === y.getTime();
	}

	if (Object.keys(x).length !== Object.keys(y).length) {
		return false;
	}

	for (const key in x) {
		if (!(key in (y as object))) {
			return false;
		}

		// @ts-expect-error TypeScript doesn't understand that 'key' is a property of both 'x' and 'y', but we check it previously.
		if (!deepEqual(x[key], y[key])) {
			return false;
		}
	}

	return true;
}

export function memoize<Args extends unknown[], Return>(
	fn: (...args: [...Args]) => Return,
	opts?: { maxSize?: number; hashKey: (...args: [...Args]) => unknown }
): (...args: [...Args]) => Return {
	let cache: { key: unknown; value: Return }[] = [];
	const maxSize = opts?.maxSize ?? 2048;
	const hashKey = opts?.hashKey ?? ((...args) => args);

	console.log('maxSize', maxSize);
	return (...args: [...Args]) => {
		const hash = hashKey(...args);
		for (const { key, value } of cache) {
			if (deepEqual(key, hash)) {
				console.log('Cache hit');
				return value;
			}
		}

		console.log('Cache miss', cache.length);
		const output = fn(...args);

		// cache.push({ key: structuredClone($state.snapshot({ ...args })), value: output });
		// console.log('putting in cache', hash)
		cache.push({ key: hash, value: output });

		// Make cache maximum size `CACHE_THRESHOLD` by removing the oldest elements
		if (cache.length > maxSize) {
			console.log('cache full, deleting');
			cache = cache.toSpliced(0, maxSize - cache.length);
		}

		return output;
	};
}
