import { expect, test } from 'vitest';
import { humanSensibleDate } from '.';

// Set a fixed date for testing
const currentDate = new Date('2024-05-17:12:00:00');

const sut = (date: Date) => humanSensibleDate(date, currentDate);

test('Different years show the year', () => {
	expect(sut(new Date('2021-05-17'))).toEqual('17 May 2021');
	expect(sut(new Date('2021-08-17'))).toEqual('17 Aug 2021');
	expect(sut(new Date('2021-08-31'))).toEqual('31 Aug 2021');
});

test('Same year skips the year', () => {
	expect(sut(new Date('2024-02-20'))).toEqual('20 Feb');
	expect(sut(new Date('2024-02-17'))).toEqual('17 Feb');
});

test('Same month still specifies month', () => {
	expect(sut(new Date('2024-05-01'))).toEqual('1 May');
	expect(sut(new Date('2024-05-05'))).toEqual('5 May');
});

test('Today or yesterday show the time', () => {
	expect(sut(new Date('2024-05-16:12:15:23:069'))).toEqual('Yesterday at 12:15');
	expect(sut(new Date('2024-05-17:10:52:22'))).toEqual('Today at 10:52');
});
