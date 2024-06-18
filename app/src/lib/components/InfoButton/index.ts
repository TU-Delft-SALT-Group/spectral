import type { ComponentType } from 'svelte';
import SimpleInfoContent from './SimpleInfoContent.svelte';
import WaveformContent from './WaveformContent.svelte';
import SpectrogramContent from './SpectrogramContent.svelte';
import VowelSpaceContent from './VowelSpaceContent.svelte';
import TranscriptionContent from './TranscriptionContent.svelte';
import ErrorRateContent from './ErrorRateContent.svelte';

export { default as InfoButton } from './InfoButton.svelte';
export const contents: { title: string; content: ComponentType }[] = [
	{ title: 'Simple Info', content: SimpleInfoContent },
	{ title: 'Waveform', content: WaveformContent },
	{ title: 'Spectrogram', content: SpectrogramContent },
	{ title: 'Vowel Space', content: VowelSpaceContent },
	{ title: 'Transcription', content: TranscriptionContent },
	{ title: 'Error-rate', content: ErrorRateContent }
];
