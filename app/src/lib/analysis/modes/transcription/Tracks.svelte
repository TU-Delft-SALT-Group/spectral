<script lang="ts">
	import type { TracksPluginOptions } from '.';

	let { tracks }: TracksPluginOptions = $props();
</script>

<div>
	{#each tracks as track}
		<div>{track}</div>
	{/each}
</div>
