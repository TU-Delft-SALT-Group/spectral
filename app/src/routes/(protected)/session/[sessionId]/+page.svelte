<script lang="ts">
	import { browser } from '$app/environment';
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PageServerData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';
	import type { SessionState } from './workspace';

	export let data: PageServerData;
	let lastUpdate: number = -Infinity;

	// for some reason it complains that timeout doesn't get used, even though it does
	let timeout: ReturnType<typeof setTimeout> | null = null;

	/**
	 * Attempt sync will try to sync with the following behaviour:
	 * - If the last sync was over 5 seconds ago, it will send data immediately to the server.
	 * - If the last sync was below 5 seconds ago, it will send data 5 seconds after the last sync.
	 */
	function attemptSync() {
		if (!browser || timeout !== null) return;

		let now = Date.now();

		timeout = setTimeout(
			() => {
				syncState(data.state);
				lastUpdate = Date.now();
				timeout = null;
			},
			5 * 1000 - (now - lastUpdate)
		);
	}

	/**
	 * This function simply sends session state to the database to be stored
	 */
	async function syncState(state: SessionState) {
		await fetch(`/db/session/${data.sessionId}`, {
			method: 'POST',
			body: JSON.stringify(state)
		});

		lastUpdate = Date.now();
	}

<<<<<<< HEAD:app/src/routes/(protected)/session/[sessionId]/+page.svelte
	$: if (data.state) {
		attemptSync();
	}

	let workspace: Workspace;
=======
	$: attemptSync(data.state);
	$: console.log(data.state);
>>>>>>> 8b9de2f (feat: working panes in session):app/src/routes/session/[sessionId]/+page.svelte
</script>

<div class="flex h-full">
	<Resizable.PaneGroup direction="horizontal">
		<Resizable.Pane defaultSize={20} minSize={11}>
			<FileExplorer
				bind:files={data.files}
				sessionId={data.sessionId}
				onDeleteFile={(fileId) => workspace.deleteFile(fileId)}
			></FileExplorer>
		</Resizable.Pane>

		<Resizable.Handle withHandle />

		<Resizable.Pane defaultSize={80}>
			<Workspace bind:state={data.state} bind:this={workspace}></Workspace>
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>
