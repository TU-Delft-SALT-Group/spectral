<script lang="ts">
	import type { Transcription } from '../file-state';
	import * as Resizable from '$lib/components/ui/resizable';
	import type { PaneGroupAPI } from 'paneforge';
	import { Button } from '$lib/components/ui/button';

	export let transcription: Transcription;
	export let duration: number;
	let paneGroup: PaneGroupAPI;

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
			value: 'work'
		};

		transcription.captions = [
			...transcription.captions.slice(0, ind + 1),
			newCaption,
			...transcription.captions.slice(ind + 1)
		];
	}

	function updateSizes(captions: Caption[]) {
		if (paneGroup === undefined || duration === undefined) {
			return;
		}

		let percentages = captions.map(({ start, end }) => (end - start) / duration);
		paneGroup.setLayout(percentages);
	}

	$: updateSizes(transcription.captions);
</script>

<div class="flex w-full flex-row items-center gap-4">
	<span>{transcription.name}</span>
	<Resizable.PaneGroup
		direction="horizontal"
		class="w-full"
		onLayoutChange={(layout) => {
			if (layout.length !== transcription.captions.length) {
				return;
			}

			console.log(layout);
		}}
		bind:paneGroup
	>
		{#if duration !== undefined}
			{#each transcription.captions as caption ([caption.start, caption.end])}
				<Resizable.Pane defaultSize={(caption.start - caption.end) / duration}>
					<Button
						class="w-full"
						variant="outline"
						onclick={(event: MouseEvent) => onClick(event, caption)}>{caption.value}</Button
					>
				</Resizable.Pane>

				{#if caption !== transcription.captions[transcription.captions.length - 1]}
					<Resizable.Handle />
				{/if}
			{/each}
		{/if}
	</Resizable.PaneGroup>
</div>
