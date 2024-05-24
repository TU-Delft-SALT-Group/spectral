<script lang="ts">
	import AnalysisPane from '$lib/analysis/AnalysisPane.svelte';
	import type { SessionState } from './workspace';

	export let state: SessionState;
</script>

<div class="h-full w-full">
	{#each state.panes as pane}
		<AnalysisPane bind:state={pane}></AnalysisPane>
	{/each}
</div>
