<script lang="ts">
	import AnalysisPane from '$lib/analysis/AnalysisPane.svelte';
	import type { WorkspaceState } from './workspace';

	export let state: WorkspaceState;
</script>

<div class="h-full w-full">
	{#each state.panes as pane}
		<AnalysisPane bind:state={pane}></AnalysisPane>
	{/each}
</div>
