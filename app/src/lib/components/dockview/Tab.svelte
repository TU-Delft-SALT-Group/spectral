<script lang="ts">
	import type { DockviewPanelApi } from 'dockview-core';
	import XIcon from 'lucide-svelte/icons/x';
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';

	export let api: DockviewPanelApi;
	export let title: string | undefined;
	let previousTitle: string | null = null;
	let titleElement: HTMLElement;

	let deleteAlertOpen = false;

	function handleClick() {
		if (titleElement.isContentEditable) {
			return;
		}

		previousTitle = titleElement.textContent;
		titleElement.contentEditable = 'true';
		window.getSelection()?.selectAllChildren(titleElement);
	}

	function handleKeydown(event: KeyboardEvent) {
		if (!titleElement.isContentEditable) {
			return;
		}

		if (event.key === 'Enter') {
			titleElement.contentEditable = 'false';
			api.setTitle(titleElement.textContent!);
		} else if (event.key === 'Escape') {
			titleElement.textContent = previousTitle;
			titleElement.contentEditable = 'false';
		}
	}
</script>

<div
	class="m-0 flex h-full w-full flex-row rounded-none bg-background bg-opacity-0 transition hover:bg-opacity-50"
>
	<button
		class="flex h-full flex-1 items-center justify-center px-1 transition focus:outline-transparent"
		on:dblclick={handleClick}
		on:keydown={handleKeydown}
	>
		<span bind:this={titleElement}>
			{title}
		</span>
	</button>
	<button
		class="ml-auto h-full cursor-pointer items-center justify-center rounded-none p-0 px-1 transition hover:bg-destructive/30"
		on:mousedown={() => deleteAlertOpen = true}
	>
		<XIcon class="h-4 w-4 text-secondary-foreground"></XIcon>
	</button>
</div>

<AlertDialog.Root bind:open={deleteAlertOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete this pane and the analysis conducted in it.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action on:click={() => api.close()}>Continue</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>
