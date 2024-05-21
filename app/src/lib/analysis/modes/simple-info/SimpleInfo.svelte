<script lang="ts">
	import type { SpecificModeData } from '..';
	import SimpleInfoSingle from './SimpleInfoSingle.svelte';

	export let data: SpecificModeData<'simple-info'>[];
</script>

<div class="grid h-full grid-cols-3 items-center gap-4 p-4">
	{#each data as data}
		<div class="w-fit max-w-2xl rounded p-4 text-secondary-foreground">
			<SimpleInfoSingle {data}></SimpleInfoSingle>
		</div>
	{/each}
</div>
