import type { mode } from '$lib/analysis/modes';
import { SpectrogramPlugin } from '$lib/analysis/modes/spectrogram';
import { WaveformPlugin } from '$lib/analysis/modes/waveform';
import type { ComponentType, SvelteComponent } from 'svelte';

export type VisualizationType = 'waveform' | 'spectrogram';

export type ControlRequirements = {
	clearRegions: () => boolean;
	togglePlay: () => void;
	pause: () => void;
	play: () => void;
	setSpeed: (speed: number) => void;
	seek: (amount: number) => void;
};

type PluginProps<M extends VisualizationType> = {
	computedData: mode.ComputedData<M>;
	fileState: mode.FileState<M>;
	duration: number;
	current: number;
	playing: boolean;
	width: number;
	controls: ControlRequirements;
	setAsSelected: () => void;
};

export type PluginComponent<T extends VisualizationType> = ComponentType<
	SvelteComponent<PluginProps<T>>
>;

export function getVisualizationComponent<M extends VisualizationType>(
	type: M
): PluginComponent<M> {
	switch (type) {
		case 'waveform':
			return WaveformPlugin as PluginComponent<M>;
		case 'spectrogram':
			return SpectrogramPlugin as PluginComponent<M>;
	}

	throw new Error('Unreachable');
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
