<script lang="ts">
	import RecorderSingle from './RecorderSingle.svelte';
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PromptResponse } from './recorder';
	import { Button } from '$lib/components/ui/button';
	import JSZip from 'jszip';
	import { toast } from 'svelte-sonner';
	import { Toaster } from '$lib/components/ui/sonner';

	export let prompts: PromptResponse[];
	export let promptName: string;
	export let recording = false;

	let selectedIndex: number = 0;
	let disableExport: boolean = false;
	let disableImport: boolean = false;

	function prependZeros(desiredLength: number, currentString: string) {
		return '0'.repeat(desiredLength - currentString.length) + currentString;
	}

	async function downloadAllRecordings() {
		disableExport = true;
		const zip = new JSZip();
		let notes = '';
		for (let prompt of prompts) {
			let promptIndexPadded = prependZeros(4, '' + prompt.index);
			let promptName = promptIndexPadded + '-' + prompt.id;
			zip.file(`${promptName}.txt`, prompt.content);
			for (let i = 0; i < prompt.recordings.length; i++) {
				let recordingName = promptIndexPadded + '-' + prependZeros(3, '' + i) + '-' + prompt.id;
				notes += recordingName + ': ' + prompt.recordings[i].note;
				zip.file(`${recordingName}.webm`, prompt.recordings[i].blob);
			}
		}
		zip.file('notes.txt', notes);
		zip
			.generateAsync({ type: 'blob' })
			.then(function (content: Blob) {
				const url = URL.createObjectURL(content);
				const a = document.createElement('a');
				a.href = url;
				a.download = `${promptName}.zip`;
				a.click();
				URL.revokeObjectURL(url);
			})
			.then(() => {
				disableExport = false;
			});
	}

	function importSession() {
		disableImport = true;
		const formData = new FormData();
		let data = [];
		for (let prompt of prompts) {
			let promptIndexPadded = prependZeros(4, '' + prompt.index);
			for (let i = 0; i < prompt.recordings.length; i++) {
				let recordingName = promptIndexPadded + '-' + prependZeros(3, '' + i) + '-' + prompt.id;
				data.push({ name: recordingName, groundTruth: prompt.content });
				formData.append(recordingName, prompt.recordings[i].blob);
			}
		}
		formData.append('data', JSON.stringify(data));
		formData.append('sessionName', promptName);
		fetch('?/importAudio', {
			method: 'POST',
			body: formData
		}).then(async (response) => {
			if (response.status == 200) {
				let data = JSON.parse((await response.json()).data);
				toast.success('Session ' + data[0] + ' has been created.', {
					description: 'Go to the session',
					action: {
						label: 'Session',
						onClick: () => {
							window.location.href = '/session/' + data[0];
						}
					}
				});
			}
			disableImport = false;
		});
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'ArrowRight') {
			next();
		} else if (event.key === 'ArrowLeft') {
			previous();
		}
	}

	const next = () =>
		!recording && (selectedIndex = Math.min(prompts.length - 1, selectedIndex + 1));
	const previous = () => !recording && (selectedIndex = Math.max(0, selectedIndex - 1));

	const windowSize = 2;
	$: center = Math.min(Math.max(windowSize, selectedIndex), prompts.length - windowSize);
</script>

<svelte:window on:keydown={handleKeydown} />

<main class="h-full">
	<Resizable.PaneGroup class="flex h-full" direction="horizontal">
		<Resizable.Pane
			class="z-30 flex flex-col gap-2 bg-secondary/50 p-4 pt-2 text-secondary-foreground"
			defaultSize={20}
		>
			<p class="text-muted-foreground">For session &lt;session-id&gt</p>

			<p>
				You have recorded {prompts.filter((prompt) => prompt.recordings.length > 0)
					.length}/{prompts.length} prompts
			</p>

			<div class="flex-1"></div>

			<Button disabled={disableImport} on:click={importSession}>Export recording to session</Button>
			<Button disabled={disableExport} on:click={downloadAllRecordings} variant="outline"
				>Save files to disk</Button
			>
		</Resizable.Pane>

		<Resizable.Handle withHandle></Resizable.Handle>

		<Resizable.Pane class="relative mx-auto h-full py-4">
			{#each prompts
				.map((prompt, i) => ({ prompt, i }))
				.slice(center - windowSize, center + windowSize + 1) as { prompt, i } (prompt.id)}
				<section
					class:unselected={i !== selectedIndex}
					style:--index={i}
					style:--selected-index={selectedIndex}
					class="absolute z-20 h-[calc(100%-theme(space.8))] w-full overflow-y-scroll text-balance rounded p-4 text-center text-secondary-foreground transition"
				>
					<RecorderSingle
						bind:prompt={prompts[i]}
						bind:recording
						focused={i === selectedIndex}
						onNext={next}
						onPrevious={previous}
					/>
				</section>
			{/each}
		</Resizable.Pane>
	</Resizable.PaneGroup>
	<Toaster />
</main>

<style lang="postcss">
	section {
		--gap: calc(theme(maxWidth.xl) + theme(space.8));
		transform: translateX(calc((var(--index) - var(--selected-index)) * var(--gap))) var(--scale);

		transition-timing-function: cubic-bezier(0.2, 1, 0.22, 1);
		transition-duration: 1.2s;
	}

	.unselected {
		--scale: scale(0.95);
		@apply pointer-events-none z-0 opacity-50;
	}
</style>
