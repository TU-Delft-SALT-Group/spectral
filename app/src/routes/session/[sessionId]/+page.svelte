<script lang="ts">
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PageServerData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';
	import type { WorkspaceState } from './workspace';

	export let data: PageServerData;
	let lastUpdate: number = 0;
	let timeout: ReturnType<typeof setTimeout> | null;

	function attemptSync(state: WorkspaceState) {
		if (!timeout) return;

		let now = Date.now();

		if (now - lastUpdate > 5 * 1000) {
			syncState(state);
			lastUpdate = now;
		} else {
			timeout = setTimeout(
				() => {
					syncState(data.state);
					lastUpdate = Date.now();
					timeout = null;
				},
				5 * 1000 - (now - lastUpdate)
			);
		}
	}

	async function syncState(state: WorkspaceState) {
		await fetch(`/db/session/${data.sessionId}`, {
			method: 'POST',
			body: JSON.stringify(state)
		});

		lastUpdate = Date.now();
	}

	$: attemptSync(data.state);
</script>

<div class="flex h-full">
	<Resizable.PaneGroup direction="horizontal">
		<Resizable.Pane defaultSize={20} minSize={11}>
			<FileExplorer files={data.files} sessionId={data.sessionId}></FileExplorer>
		</Resizable.Pane>

		<Resizable.Handle withHandle />

		<Resizable.Pane defaultSize={80}>
			<Workspace bind:state={data.state}></Workspace>
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>
