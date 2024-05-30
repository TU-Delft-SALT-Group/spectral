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

	export let files: FileState[];
	export let sessionId: string;
	export let onDeleteFile: (fileId: string) => void;

	let submitButton: HTMLInputElement;
</script>

<div class="flex h-full flex-col">
	<ol class="flex-1 py-2">
		{#each files as file (file.id)}
			<li
				class="px-2 py-1"
				animate:flip={{ duration: 400 }}
				transition:fade={{ duration: 400 }}
				draggable={true}
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
				></FileEntry>
			</li>
		{:else}
			<div class="text-muted-foreground w-full text-center py-3">No files yet!</div>
		{/each}
	</ol>

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
