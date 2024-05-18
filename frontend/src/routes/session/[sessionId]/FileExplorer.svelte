<!--
	@component

	File explorer for the audio files.
-->

<script lang="ts">
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import { Separator } from '$lib/components/ui/separator';
	import { Input } from '$lib/components/ui/input';
	import * as ContextMenu from '$lib/components/ui/context-menu';
	import { getFileIcon, type FilebrowserFile } from '$lib/files';
	import { cn } from '$lib/utils';
	import { enhance } from '$app/forms';
	import { MicIcon } from 'lucide-svelte';
	import { invalidateAll } from '$app/navigation';
	import { flip } from 'svelte/animate';
	import { fade } from 'svelte/transition';

	export let files: FilebrowserFile[];

	new Date().toLocaleString('en-GB', {
		minute: '2-digit',
		second: '2-digit',
		fractionalSecondDigits: 3
	});

	let submitButton: HTMLInputElement;

	// Manual fetch because it's a hassle to set up the form
	async function deleteFile(fileId: string) {
		await fetch('?/deleteFile', { method: 'POST', body: JSON.stringify({ fileId }) });
		await invalidateAll();
	}
</script>

<div class="flex h-full flex-col">
	<ol class="flex-1 py-2">
		{#each files as file (file.id)}
			<li class="px-2 py-1" animate:flip={{ duration: 400 }} transition:fade={{ duration: 400 }}>
				<ContextMenu.Root>
					<ContextMenu.Trigger>
						<Button class="flex-2 w-full justify-start gap-2 rounded" variant="ghost">
							<svelte:component this={getFileIcon(file.type)} class="h-6 w-6"></svelte:component>
							<span class="overflow-hidden text-ellipsis">
								{file.name}
							</span>
						</Button>
					</ContextMenu.Trigger>

					<ContextMenu.Content>
						<ContextMenu.Item on:click={() => deleteFile(file.id)}>
							<span> Delete </span>
						</ContextMenu.Item>
					</ContextMenu.Content>
				</ContextMenu.Root>
			</li>
		{:else}
			<div class="text-muted-foreground w-full text-center py-3">No files yet!</div>
		{/each}
	</ol>

	<Separator class=""></Separator>

	<div class="h-fit p-4">
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

		<Button class="w-full bg-red-800 bg-opacity-80 text-white shadow hover:bg-red-700">
			<MicIcon class="h-5 w-5"></MicIcon>
			<span class="pl-2"> Record </span>
		</Button>
	</div>
</div>
