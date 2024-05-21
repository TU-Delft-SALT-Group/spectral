import { z } from 'zod';

export const spectrogramData = z.object({
	mode: z.literal('spectrogram')
});

export { default as Spectrogram } from './Spectrogram.svelte';
export { default as SpectrogramIcon } from './SpectrogramIcon.svelte';
export { default as SpectrogramPlugin } from './SpectrogramPlugin.svelte';
