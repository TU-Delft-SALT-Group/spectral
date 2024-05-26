<script lang="ts">
	import AnalysisPane from '$lib/analysis/AnalysisPane.svelte';
	import type { SessionState } from './workspace';

	export let state: SessionState;
	let panes: (null | AnalysisPane)[] = state.panes.map(() => null);

	export function deleteFile(fileId: string) {
		for (const pane of panes) {
			pane?.removeFile(fileId);
		}
	}
</script>

<div class="h-full w-full">
	{#each state.panes as paneState, i}
		<AnalysisPane bind:this={panes[i]} bind:state={paneState}></AnalysisPane>
	{/each}
</div>
