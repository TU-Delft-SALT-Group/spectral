import { unwrap } from '$lib/utils';

/**
 * Units of file size, up to terabytes.
 */
export const units = (() => {
	const ladder = [
		['bytes', 'B'],
		['kilobytes', 'KB'],
		['megabytes', 'MB'],
		['gigabytes', 'GB'],
		['terabytes', 'TB']
	] as const;

	return ladder.map(([unit, short], i) => ({
		unit,
		short,
		value: 1000 ** i
	})) as {
		unit: (typeof ladder)[number][0];
		short: (typeof ladder)[number][1];
		value: number;
	}[];
})();

/**
 * Get a unit by name.
 */
export function unit(name: UnitName): Unit {
	return unwrap(units.find((unit) => unit.unit === name));
}

export type Unit = (typeof units)[number];

export type UnitName = (typeof units)[number]['unit'];

/**
 * Convert a number of bytes to a human-readable file size.
 */
export function humanSensibleFileSize(bytes: number) {
	const unit =
		units.find((unit) => bytes < 1000 * unit.value && bytes >= unit.value) ?? unwrap(units.at(-1));
	const value = bytes / unit.value;

	return {
		unit,
		value
	};
}

/**
 * Convert a number of bytes to a human-readable file size.
 */
export function formatHumanSensibleFileSize(bytes: number) {
	const { unit, value } = humanSensibleFileSize(bytes);
	const order = Math.floor(Math.log10(value));
	return `${value.toFixed(2 - order)} ${unit.short}`;
}
