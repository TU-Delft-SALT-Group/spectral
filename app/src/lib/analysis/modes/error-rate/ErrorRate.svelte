<script lang="ts">
	import type { ModeComponentProps } from '..';
	import used from '$lib/utils';
	import ErrorRatePlugin from './ErrorRatePlugin.svelte';

	export let fileData: ModeComponentProps<'error-rate'>['fileData'];
	export let modeState: ModeComponentProps<'error-rate'>['modeState'];

	used(modeState);
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	{#each fileData as { computedData, fileState } (fileState.id)}
		<ErrorRatePlugin {computedData} {fileState} />
	{/each}
</section>
