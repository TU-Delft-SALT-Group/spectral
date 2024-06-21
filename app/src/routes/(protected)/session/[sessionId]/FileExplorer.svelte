<!--
	@component

	File explorer for the audio files.
-->

<script lang="ts">
	import { buttonVariants } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { Input } from '$lib/components/ui/input';
	import { cn } from '$lib/utils';
	import { enhance } from '$app/forms';
	import { flip } from 'svelte/animate';
	import { fade } from 'svelte/transition';
	import Recorder from './Recorder.svelte';
	import FileEntry from './FileEntry.svelte';
	import type { FileState } from '$lib/analysis/modes/file-state';
	import Workspace from './Workspace.svelte';

	export let workspace: Workspace | undefined;

	export let files: FileState[];
	export let sessionId: string;
	export let onDeleteFile: (fileId: string) => void;

	let filesContextMenu: boolean[] = [];
	let submitButton: HTMLInputElement;

	function closeAllContextMenus() {
		for (let i = 0; i < filesContextMenu.length; i++) {
			filesContextMenu[i] = false;
		}
	}
</script>

<div class="flex h-full flex-col bg-secondary/75 text-secondary-foreground">
	<div class="h-full flex-1 flex-col py-2">
		{#each files as file, i (file.id)}
			<button
				class="w-full px-2 py-1"
				animate:flip={{ duration: 400 }}
				transition:fade={{ duration: 400 }}
				draggable={true}
				on:click={() => {
					workspace?.addFileJSON(JSON.stringify(file));
				}}
				on:dragstart={(event) => {
					event.dataTransfer?.setData('application/json', JSON.stringify(file));
					if (event.dataTransfer) {
						event.dataTransfer.dropEffect = 'copy';
					}
				}}
			>
				<FileEntry
					{file}
					onDeleteFile={() => {
						onDeleteFile(file.id);
						files = files.filter((f) => f.id !== file.id);
					}}
					bind:contextMenuOpen={filesContextMenu[i]}
					{closeAllContextMenus}
				/>
			</button>
		{:else}
			<div class="text-muted-foreground w-full text-center py-3">No files yet!</div>
		{/each}
	</div>

	<Separator class=""></Separator>

	<div class="relative h-fit p-4">
		<form
			method="POST"
			use:enhance
			action="?/uploadFile"
			enctype="multipart/form-data"
			class="mb-2"
		>
			<Input
				name="file"
				type="file"
				multiple
				accept="audio/*"
				class={cn(buttonVariants({ variant: 'ghost' }))}
				on:change={() => submitButton.click()}
			/>
			<input bind:this={submitButton} type="submit" class="hidden" />
		</form>

		<Recorder {sessionId}></Recorder>
	</div>
</div>
