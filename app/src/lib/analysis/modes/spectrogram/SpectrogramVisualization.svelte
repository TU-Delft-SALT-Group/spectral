<script lang="ts">
	import { onMount } from 'svelte';
	import { calculateFrequencies } from '.';

	export let dimensions: { width: number; height: number } = { width: 0, height: 200 };
	export let file: string;

	const audioCtx = new AudioContext();

	let canvasElement: HTMLCanvasElement;
	let context: CanvasRenderingContext2D;
	let frequencies: Float32Array[];

	const samples = 4096;

	onMount(async () => {
		context = canvasElement.getContext('2d')!;
		context.canvas.width = dimensions.width;
		context.canvas.height = dimensions.height;
		context.clearRect(0, 0, dimensions.width, dimensions.height);

		const arrayBuffer = await (await fetch(`/db/file/${file}`)).arrayBuffer();
		const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer);

		frequencies = calculateFrequencies(audioBuffer, samples, audioBuffer.length / dimensions.width);

		spectroDraw();
	});

	function spectroDraw() {
		// background
		context.fillStyle = 'rgb(200 200 200)';
		context.fillRect(0, 0, dimensions.width, dimensions.height);

		const xFactor = frequencies.length / dimensions.width;
		let yFactor = frequencies[0].length / Math.log(dimensions.height);

		for (let x = 0; x < dimensions.width; x++) {
			for (let y = 0; y < dimensions.height; y++) {
				let coords = [Math.floor(x * xFactor), Math.round(Math.log(Math.max(y, 1)) * yFactor)];
				let val = frequencies[coords[0]][coords[1]];

				val *= 255;

				if (val < 0 || val > 255) throw Error(`val was ${val}`);

				val = 255 - val;

				context.fillStyle = `rgb(${val} ${val} ${val})`;
				context.fillRect(x, y, x + 1, y + 1);
			}
		}
	}
</script>

<section bind:clientWidth={dimensions.width} class="w-full">
	<canvas bind:this={canvasElement} style:height={dimensions.height}> </canvas>
</section>
