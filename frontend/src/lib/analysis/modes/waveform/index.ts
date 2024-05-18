import { z } from 'zod';

export const waveformData = z.object({
	mode: z.literal('waveform')
});

export { default as Waveform } from './Waveform.svelte';

export type WaveColor = {
	wave: string;
	progress: string;
};
