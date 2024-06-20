<script lang="ts">
	import { browser } from '$app/environment';
	import { uploadingStateStore } from '$lib';
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PageData } from './$types';
	import FileExplorer from './FileExplorer.svelte';
	import Workspace from './Workspace.svelte';
	import type { SessionState } from './workspace';
	import { beforeNavigate } from '$app/navigation';

	export let data: PageData;
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
		uploadingStateStore.set(true);

		let now = Date.now();

		timeout = setTimeout(
			() => {
				syncState(data.state);
				lastUpdate = Date.now();
				timeout = null;
				uploadingStateStore.set(false);
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

	$: if (data && data.state) {
		attemptSync();
	}

	// subscribe to our own loading store lol
	let loading: boolean = true;
	uploadingStateStore.subscribe((val) => {
		loading = val;
	});

	// Send alert if closing while loading
	beforeNavigate(({ type, cancel }) => {
		if (loading) {
			// sync ASAP, but don't block the thread
			syncState(data.state);

			if (type === 'leave') {
				// if leaving: nicely suggest to wait
				cancel();
			}

			// if any other type of leaving (probably local link)
			// we actually don't care, since the async process was triggered
			// so the saving will continue even after you moved
		}
	});

	let workspace: Workspace;
</script>

<svelte:head>
	<title>{data.name}</title>
</svelte:head>

<div class="flex h-full w-screen">
	<Resizable.PaneGroup direction="horizontal">
		<Resizable.Pane defaultSize={20} minSize={11} collapsible={true} collapsedSize={1}>
			<FileExplorer
				bind:files={data.files}
				bind:workspace
				sessionId={data.sessionId}
				onDeleteFile={(fileId) => workspace.deleteFile(fileId)}
			></FileExplorer>
		</Resizable.Pane>

		<Resizable.Handle withHandle />

		<Resizable.Pane defaultSize={80}>
			<Workspace bind:workspaceState={data.state} bind:this={workspace}></Workspace>
		</Resizable.Pane>
	</Resizable.PaneGroup>
</div>
