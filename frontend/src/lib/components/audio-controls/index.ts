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

export function getVisual(visual: VisualizationType): ComponentType {
	switch (visual) {
		case 'waveform':
			return WaveformPlugin;
		case 'spectrogram':
			return SpectrogramPlugin;
	}
}
