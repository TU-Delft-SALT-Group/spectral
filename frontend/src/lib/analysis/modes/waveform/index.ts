import { z } from 'zod';

export const waveformData = z.object({
	mode: z.literal('waveform')
});

export { default as Waveform } from './Waveform.svelte';
export { default as WaveformPlugin } from './WaveformPlugin.svelte';

export type WaveColor = {
	wave: string;
	progress: string;
};
