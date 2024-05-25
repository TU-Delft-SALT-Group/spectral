<script lang="ts">
	import { browser } from '$app/environment';
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PageServerData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';
	import type { SessionState } from './workspace';

	export let data: PageServerData;
	let lastUpdate: number = 0;

	// for some reason it complains that timeout doesn't get used, even though it does
	// eslint-disable-next-line
	let timeout: ReturnType<typeof setTimeout> | null = null;

	/**
	 * Attempt sync will try to sync with the following behaviour:
	 * - If the last sync was over 5 seconds ago, it will send data immediately to the server.
	 * - If the last sync was below 5 seconds ago, it will send data 5 seconds after the last sync.
	 */
	function attemptSync(state: SessionState) {
		if (!browser || timeout !== null) return;

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
