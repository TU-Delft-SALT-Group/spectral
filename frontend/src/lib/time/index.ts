const LOCALE = 'en-GB';

/**
 * Converts a date to a human sensible date format.
 *
 * That is, it doesn't show a period if that period is the same as the current one
 */
export function humanSensibleDate(date: Date, currentDate = new Date()): string {
	const msInDay = 1000 * 60 * 60 * 24;
	const day = (date: Date) => Math.floor(date.getTime() / msInDay);

	const dayDiff = day(currentDate) - day(date);

	if (dayDiff <= 1) {
		const day = dayDiff === 0 ? 'Today' : 'Yesterday';
		const time = date.toLocaleString(LOCALE, { hour: '2-digit', minute: '2-digit' });

		return `${day} at ${time}`;
	}

	const year = currentDate.getFullYear() === date.getFullYear() ? undefined : 'numeric';

	return date.toLocaleDateString(LOCALE, {
		day: 'numeric',
		month: 'short',
		year
	});
}
