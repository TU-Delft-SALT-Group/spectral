import { z } from 'zod';
import type { ModeValidator } from '..';
import { fileState } from '../file-state';
import webfft from 'webfft';

export const spectrogramData = {
	computedFileData: z.object({ formants: z.array(z.array(z.number().nullable())).nullable() }),

	fileState: fileState
		.pick({
			id: true,
			name: true,
			frame: true
		})
		.default({}),

	modeState: z.object({}).default({})
} satisfies ModeValidator;

/**
 * Very simple cosine window function
 */
function createWindow(samples: number): number[] {
	const ret: number[] = [];

	for (let i = 0; i < samples; i++) {
		ret[i] = Math.cos((Math.PI * i) / (samples - 1) - Math.PI / 2);
	}

	return ret;
}

export function calculateFrequencies(
	audioData: AudioBuffer,
	samples: number,
	step: number
): Float32Array[] {
	const fft = new webfft(samples);
	const ret: Float32Array[] = [];
	const windowFunc = createWindow(samples);

	// we assume that audio has only 1 channel
	const data = audioData.getChannelData(0);
	let maxValue: number = -Infinity;

	for (let offset = 0; offset + samples < data.length; offset += step) {
		const segment = data.slice(offset, offset + samples).map((x, i) => x * windowFunc[i]);
		// @ts-expect-error for some reason fftr isn't visible to us even though we can use it
		const transformation: Float32Array = fft.fftr(segment);

		const out: Float32Array = new Float32Array(samples / 2);

		for (let i = 0; i < transformation.length; i += 2) {
			let val =
				transformation[i] * transformation[i] + transformation[i + 1] * transformation[i + 1];
			if (val < 0) throw Error(`val was: ${val}`);
			val = Math.sqrt(val);
			val = Math.pow(5, -val);
			// val = Math.tanh(val);
			maxValue = Math.max(maxValue, val);

			out[i / 2] = val;
		}

		ret.push(out);
	}

	const resolution = 100000;

	for (let i = 0; i < ret.length; i++) {
		for (let j = 0; j < ret[0].length; j++) {
			ret[i][j] /= maxValue;
			ret[i][j] = Math.floor(ret[i][j] * resolution) / resolution;
		}
	}

	return ret;
}

export function clamp(number: number, min: number, max: number): number {
	return Math.min(Math.max(number, min), max);
}

export { default as Spectrogram } from './Spectrogram.svelte';
export { default as SpectrogramIcon } from './SpectrogramIcon.svelte';
export { default as SpectrogramPlugin } from './SpectrogramPlugin.svelte';
