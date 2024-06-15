import { SpectrogramPlugin } from '$lib/analysis/modes/spectrogram';
import { WaveformPlugin } from '$lib/analysis/modes/waveform';
import type { ComponentType } from 'svelte';

export type VisualizationType = 'waveform' | 'spectrogram';

export type ControlRequirements = {
	clearRegions: () => boolean;
	togglePlay: () => void;
	pause: () => void;
	play: () => void;
	setSpeed: (speed: number) => void;
	seek: (amount: number) => void;
};

const pluginsRecord: Record<VisualizationType, ComponentType> = {
	waveform: WaveformPlugin,
	spectrogram: SpectrogramPlugin
};

export function getVisualizationPlugin(type: VisualizationType): ComponentType {
	return pluginsRecord[type];
}

// TODO: implement a better method in time.ts
export function numberToTime(current: number): string {
	if (current === undefined) current = 0;

	const time = new Date(current * 1000);

	return time.toLocaleString('en-GB', {
		minute: '2-digit',
		second: '2-digit',
		fractionalSecondDigits: 3
	});
}
