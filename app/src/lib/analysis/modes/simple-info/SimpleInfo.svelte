<script lang="ts">
	import used from '$lib/utils';
	import type { ModeComponentProps } from '..';
	import SimpleInfoSingle from './SimpleInfoSingle.svelte';

	export let fileData: ModeComponentProps<'simple-info'>['fileData'];
	export let modeState: ModeComponentProps<'simple-info'>['modeState'];

	used(modeState);
</script>

<div class="grid h-full grid-cols-3 items-center gap-4 p-4">
	{#each fileData as { fileState, computedData }}
		<div class="w-fit max-w-2xl rounded p-4 text-secondary-foreground">
			<SimpleInfoSingle {computedData} {fileState}></SimpleInfoSingle>
		</div>
	{/each}
</div>
