<script lang="ts">
	import type { SpecificModeData } from '..';
	import SimpleInfoSingle from './SimpleInfoSingle.svelte';

	export let data: SpecificModeData<'simple-info'>[];
</script>

{#each data as data}
	<SimpleInfoSingle {data}></SimpleInfoSingle>
{/each}
