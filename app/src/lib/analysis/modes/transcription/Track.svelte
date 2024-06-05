<script lang="ts">
	import type { Transcription } from '../file-state';
	import * as Resizable from '$lib/components/ui/resizable';
	import { Button } from '$lib/components/ui/button';
	import type { PaneGroupAPI } from 'paneforge';

	let {
		transcription,
		duration
	}: {
		transcription: Transcription;
		duration: number;
	} = $props();

	let paneGroup: PaneGroupAPI | undefined = $state(undefined);
	let handleElementList: HTMLElement[] = $state([]);
	let currentlyHeldButton: HTMLElement | null = null;

	$effect(() => {
		if (handleElementList === null) {
			return;
		}

		for (const element of handleElementList) {
			element.onmousedown = () => {
				currentlyHeldButton = element;
			};
		}
	});

	type Caption = {
		start: number;
		end: number;
		value: string;
	};

	function onClick(event: MouseEvent, caption: Caption) {
		event.preventDefault();
		event.stopImmediatePropagation();

		let boundingBox = (event.target! as HTMLElement).getBoundingClientRect();
		let percentage = (event.x - boundingBox.left) / boundingBox.width;
		let oldEnd = caption.end;
		let ind = transcription.captions.indexOf(caption);

		caption.end = caption.start + (caption.end - caption.start) * percentage;

		let newCaption: Caption = {
			start: caption.end,
			end: oldEnd,
			value: ''
		};

		transcription.captions = [
			...transcription.captions.slice(0, ind + 1),
			newCaption,
			...transcription.captions.slice(ind + 1)
		];
	}
</script>

<div class="flex w-full flex-row items-center gap-4">
	<span>{transcription.name}</span>
	<Resizable.PaneGroup direction="horizontal" class="w-full" bind:paneGroup>
		{#if duration !== undefined}
			{#each transcription.captions as caption, i ([caption.start, caption.end])}
				<Resizable.Pane class="w-full" defaultSize={(caption.start - caption.end) / duration}>
					<Button
						class="w-full rounded-none"
						variant="outline"
						onclick={(event: MouseEvent) => onClick(event, caption)}>{caption.value}</Button
					>
				</Resizable.Pane>

				{#if caption !== transcription.captions[transcription.captions.length - 1]}
					<Resizable.Handle bind:el={handleElementList[i]}></Resizable.Handle>
				{/if}
			{/each}
		{/if}
	</Resizable.PaneGroup>
</div>

<svelte:window
	on:mouseup={(e) => {
		if (currentlyHeldButton === null || paneGroup === undefined) {
			return;
		}

		e.preventDefault();

		let captions = transcription.captions;
		let layout = paneGroup.getLayout();
		let prevEnd = 0;

		for (let i = 0; i < layout.length; i++) {
			captions[i].start = prevEnd;
			captions[i].end = prevEnd + duration * (layout[i] / 100);
			prevEnd = captions[i].end;
		}

		transcription.captions = captions;
		currentlyHeldButton = null;

		return;
	}}
/>
