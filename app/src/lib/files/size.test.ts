import { expect, test } from 'vitest';
import { formatHumanSensibleFileSize, humanSensibleFileSize, unit } from './size';

test('Show correct units and value', () => {
	expect(humanSensibleFileSize(24)).toEqual({
		value: 24,
		unit: unit('bytes')
	});

	expect(humanSensibleFileSize(999)).toEqual({
		value: 999,
		unit: unit('bytes')
	});

	expect(humanSensibleFileSize(1000)).toEqual({
		value: 1,
		unit: unit('kilobytes')
	});

	expect(humanSensibleFileSize(1024)).toEqual({
		value: 1.024,
		unit: unit('kilobytes')
	});

	expect(humanSensibleFileSize(999_000)).toEqual({
		value: 999,
		unit: unit('kilobytes')
	});

	expect(humanSensibleFileSize(1_000_000)).toEqual({
		value: 1,
		unit: unit('megabytes')
	});

	expect(humanSensibleFileSize(1_024_000)).toEqual({
		value: 1.024,
		unit: unit('megabytes')
	});

	expect(humanSensibleFileSize(999_000_000)).toEqual({
		value: 999,
		unit: unit('megabytes')
	});

	expect(humanSensibleFileSize(1_000_000_000)).toEqual({
		value: 1,
		unit: unit('gigabytes')
	});

	expect(humanSensibleFileSize(1_024_000_000)).toEqual({
		value: 1.024,
		unit: unit('gigabytes')
	});

	expect(humanSensibleFileSize(999_000_000_000)).toEqual({
		value: 999,
		unit: unit('gigabytes')
	});

	expect(humanSensibleFileSize(1_000_000_000_000)).toEqual({
		value: 1,
		unit: unit('terabytes')
	});

	expect(humanSensibleFileSize(1_024_000_000_000)).toEqual({
		value: 1.024,
		unit: unit('terabytes')
	});

	expect(humanSensibleFileSize(1_024_000_000_000_000)).toEqual({
		value: 1024,
		unit: unit('terabytes')
	});

	expect(humanSensibleFileSize(1_024_000_000_000_000_000)).toEqual({
		value: 1_024_000,
		unit: unit('terabytes')
	});
});

test('Show correct digits in format', () => {
	expect(formatHumanSensibleFileSize(1_024_000_000_000)).toEqual('1.02 TB');
	expect(formatHumanSensibleFileSize(1024)).toEqual('1.02 KB');
	expect(formatHumanSensibleFileSize(999)).toEqual('999 B');
	expect(formatHumanSensibleFileSize(950)).toEqual('950 B');
	expect(formatHumanSensibleFileSize(42)).toEqual('42.0 B');
	expect(formatHumanSensibleFileSize(12_345)).toEqual('12.3 KB');
	expect(formatHumanSensibleFileSize(12_395)).toEqual('12.4 KB');
	expect(formatHumanSensibleFileSize(2_345)).toEqual('2.35 KB');
	expect(formatHumanSensibleFileSize(2_344)).toEqual('2.34 KB');
});
