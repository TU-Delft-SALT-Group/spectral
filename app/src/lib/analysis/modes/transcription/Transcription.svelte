<script lang="ts">
	import used from '$lib/utils';
	import type { ModeComponentProps } from '..';
	import TranscriptionPlugin from './TranscriptionPlugin.svelte';

	export let fileData: ModeComponentProps<'transcription'>['fileData'];
	export let modeState: ModeComponentProps<'transcription'>['modeState'];

	used(modeState);
</script>

<section class="flex h-full w-full flex-col gap-6 p-6">
	<TranscriptionPlugin {...fileData[0]} />
</section>
