<script lang="ts">
	import type { Common } from '.';

	export let common: Common;
	export let joinString: string;

	const colors = {
		equal: 'dark:text-lime-400  dark:bg-transparent bg-lime-400',
		insert: 'dark:text-sky-400   dark:bg-transparent bg-sky-400',
		delete: 'dark:text-red-400   dark:bg-transparent bg-red-400',
		substitute: 'dark:text-amber-500 dark:bg-transparent bg-amber-500'
	};

	function getNumberArray(n: number) {
		return Array.from({ length: n }, (_, i) => i);
	}

	function joinSubstitution(
		left: string[],
		right: string[],
		leftStart: number,
		rightStart: number,
		amount: number
	): string {
		let ret = '';

		for (const i of getNumberArray(amount)) {
			const amount = Math.max(left[leftStart + i].length - right[rightStart + i].length, 0);

			ret += joinString + '_'.repeat(amount) + right[rightStart + i];
		}

		return ret;
	}

	function joinedSegment(strings: string[], start: number, end: number, replace: boolean): string {
		let ret = strings.slice(start, end).join(joinString);
		if (replace) ret = ret.replaceAll(/\S/g, '_');

		if (ret[0] === ' ') ret = '\u00A0' + ret.substring(1);
		if (ret[ret.length - 1] === ' ') ret = ret.substring(0, ret.length - 1) + '\u00A0';

		return ret;
	}
</script>

<div>
	<div class="flex flex-col font-sans">
		<span>hits: {common.hits}</span>
		<span>substitutions: {common.substitutions}</span>
		<span>deletions: {common.deletions}</span>
		<span>insertions: {common.insertions}</span>
	</div>

	<section class="flex flex-col overflow-x-auto font-mono text-xl tracking-wider">
		<!-- This one is for showing the reference -> hypothesis -->
		<h4 class="border-box flex whitespace-nowrap">
			Ref: 
			{#each common.alignments as alignment}
				<div class="w-fit {colors[alignment.type]}">
					{#if alignment.type === 'substitute'}
						{@const indexDifference = alignment.hypothesisEndIndex - alignment.hypothesisStartIndex}
						{joinSubstitution(
							common.hypothesis,
							common.reference,
							alignment.hypothesisStartIndex,
							alignment.referenceStartIndex,
							indexDifference
						)}
					{:else if alignment.type === 'insert'}
						{joinedSegment(
							common.hypothesis,
							alignment.hypothesisStartIndex,
							alignment.hypothesisEndIndex,
							true
						)}
					{:else}
						{joinedSegment(
							common.reference,
							alignment.referenceStartIndex,
							alignment.referenceEndIndex,
							false
						)}
					{/if}
				</div>
				{#if joinString !== ''}
					<div>&nbsp</div>
				{/if}
			{/each}
		</h4>
		<h4 class="border-box flex whitespace-nowrap">
			Hyp:
			<!-- This one is for showing the  hypothesis -> reference -->
			{#each common.alignments as alignment}
				<div class="w-fit {colors[alignment.type]}">
					{#if alignment.type === 'substitute'}
						{@const indexDifference = alignment.hypothesisEndIndex - alignment.hypothesisStartIndex}
						{joinSubstitution(
							common.reference,
							common.hypothesis,
							alignment.referenceStartIndex,
							alignment.hypothesisStartIndex,
							indexDifference
						)}
					{:else if alignment.type === 'delete'}
						{joinedSegment(
							common.reference,
							alignment.referenceStartIndex,
							alignment.referenceEndIndex,
							true
						)}
					{:else}
						{joinedSegment(
							common.hypothesis,
							alignment.hypothesisStartIndex,
							alignment.hypothesisEndIndex,
							false
						)}
					{/if}
				</div>
				{#if joinString !== ''}
					<div>&nbsp</div>
				{/if}
			{/each}
		</h4>
	</section>
</div>
