<script lang="ts">
	import type { RendererProps } from '..';
	import WaveformSingle from './WaveformSingle.svelte';

	export let props: RendererProps<'waveform'>;
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each props as { data, state, frame }}
		<WaveformSingle {item} bind:frame></WaveformSingle>
	{/each}
</section>
