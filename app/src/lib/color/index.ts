export function getColorByHue(hue: number): string {
	return `hsl(${hue}, 70%, 50%)`;
}

export function getPaletteColor(index: number): string {
	const hue = (index * 30 * Math.SQRT2) % 360;
	return getColorByHue(hue);
}
