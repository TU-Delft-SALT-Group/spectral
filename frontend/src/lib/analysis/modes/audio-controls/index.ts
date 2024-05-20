import type { ComponentType } from 'svelte';
import { WaveformPlugin } from '../waveform';

export type VisualizationType = 'waveform';

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
	}
}
