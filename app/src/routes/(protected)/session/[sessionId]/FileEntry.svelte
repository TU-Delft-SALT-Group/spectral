<script lang="ts">
	import * as AlertDialog from '$lib/components/ui/alert-dialog/index.js';
	import * as ContextMenu from '$lib/components/ui/context-menu';
	import * as Dialog from '$lib/components/ui/dialog';
	import FileIcon from 'lucide-svelte/icons/file';
	import type { FileState } from '$lib/analysis/modes/file-state';
	import { Input } from '$lib/components/ui/input';

	let deleteAlertOpen = false;
	let renameDialogOpen = false;
	let tempName: string;
	export let file: FileState;
	export let onDeleteFile: (fileId: string) => void = () => {};
	export let contextMenuOpen = false;
	export let closeAllContextMenus: () => void;

	// Manual fetch because it's a hassle to set up the form
	async function deleteFile(fileId: string) {
		onDeleteFile(fileId);
		await fetch('?/deleteFile', { method: 'POST', body: JSON.stringify({ fileId }) });
	}

	async function updateFilename(fileId: string, name: string) {
		await fetch('?/renameFile', { method: 'POST', body: JSON.stringify({ fileId, name }) });
	}
</script>

<ContextMenu.Root
	bind:open={contextMenuOpen}
	onOpenChange={(opened) => {
		if (!opened) return;

		closeAllContextMenus();

		contextMenuOpen = true;
	}}
>
	<ContextMenu.Trigger>
		<div
			class="flex-2 inline-flex h-10 w-full items-center justify-center gap-2 whitespace-nowrap rounded-md px-4 py-2 text-left text-sm font-medium ring-offset-background transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50"
		>
			<FileIcon />
			<span class="max-w-full flex-1 overflow-hidden text-ellipsis">
				{file.name}
			</span>
		</div>
	</ContextMenu.Trigger>

	<ContextMenu.Content>
		<ContextMenu.Item on:click={() => (renameDialogOpen = true)}>Rename</ContextMenu.Item>
		<ContextMenu.Item
			><a href={`/db/file/${file.id}`} download={file.name}>Download</a></ContextMenu.Item
		>
		<ContextMenu.Item on:click={() => (deleteAlertOpen = true)}
			><span>Delete</span></ContextMenu.Item
		>
	</ContextMenu.Content>
</ContextMenu.Root>

<AlertDialog.Root bind:open={deleteAlertOpen}>
	<AlertDialog.Content>
		<AlertDialog.Header>
			<AlertDialog.Title>Are you absolutely sure?</AlertDialog.Title>
			<AlertDialog.Description>
				This action cannot be undone. This will permanently delete the file from our servers.
			</AlertDialog.Description>
		</AlertDialog.Header>
		<AlertDialog.Footer>
			<AlertDialog.Cancel>Cancel</AlertDialog.Cancel>
			<AlertDialog.Action on:click={() => deleteFile(file.id)}>Continue</AlertDialog.Action>
		</AlertDialog.Footer>
	</AlertDialog.Content>
</AlertDialog.Root>

<Dialog.Root bind:open={renameDialogOpen}>
	<Dialog.Content>
		<Dialog.Header>
			<Dialog.Title>Rename File</Dialog.Title>
		</Dialog.Header>
		<Input
			placeholder={file.name}
			bind:value={tempName}
			on:keydown={(e) => {
				if (e.key !== 'Enter' || tempName === undefined || tempName.length === 0) {
					return;
				}

				updateFilename(file.id, tempName);
				file.name = tempName;
				renameDialogOpen = false;
			}}
		/>
	</Dialog.Content>
</Dialog.Root>
