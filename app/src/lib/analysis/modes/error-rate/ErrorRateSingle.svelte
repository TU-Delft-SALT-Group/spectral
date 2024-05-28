<script lang="ts">
	import type { mode } from '..';

	export let computedData: mode.ComputedData<'error-rate'>;
	export let fileState: mode.FileState<'error-rate'>;

	export function getNumberArray(n: number) {
		return Array.from({ length: n }, (_, i) => i); // eslint-disable-line @typescript-eslint/no-unused-vars
	}
</script>

<div class="min-w-sm h-fit max-w-4xl flex-1 rounded bg-secondary p-4 text-secondary-foreground">
	<h2>name: {fileState.name}</h2>
	<h2>id: {fileState.id}</h2>
	{#if computedData !== null}
		<h2>ground truth: {computedData.groundTruth}</h2>
		<div>
			{#each computedData.errorRates as errorRate}
				<div class="flex-1">
					<span>wer: {(errorRate.wordLevel.wer * 100).toFixed(2) + '%'}</span>
					<span>mer: {(errorRate.wordLevel.mer * 100).toFixed(2) + '%'}</span>
					<span>wil: {(errorRate.wordLevel.wil * 100).toFixed(2) + '%'}</span>
					<span>wip: {(errorRate.wordLevel.wip * 100).toFixed(2) + '%'}</span>
				</div>
				<div class="flex-1">
					<span>hits: {errorRate.wordLevel.hits}</span>
					<span>substitutions: {errorRate.wordLevel.substitutions}</span>
					<span>deletions: {errorRate.wordLevel.deletions}</span>
				</div>
				<div class="border-box overflow-x-auto font-mono">
					<h4 class="whitespace-nowrap">
						{#each errorRate.wordLevel.alignments as alignment}
							{#if alignment.type === 'equal'}
								<span class="bg-lime-400">
									{errorRate.wordLevel.reference
										.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
										.reduce((acc, cur) => acc + ' ' + cur, '')}
								</span>
							{:else if alignment.type === 'delete'}
								<span class="bg-red-600">
									{errorRate.wordLevel.reference
										.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
										.reduce((acc, cur) => acc + ' ' + cur, '')}
								</span>
							{:else if alignment.type === 'insert'}
								<span class="bg-sky-400">
									{errorRate.wordLevel.hypothesis
										.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
										.reduce((acc, cur) => acc + ' ' + cur, '')
										.replaceAll(/\S/g, '_')}
								</span>
							{:else if alignment.type === 'substitute'}
								<span class="bg-amber-500">
									{#each getNumberArray(alignment.hypothesisEndIndex - alignment.hypothesisStartIndex) as i}
										{' ' +
											'_'.repeat(
												Math.max(
													errorRate.wordLevel.hypothesis[alignment.hypothesisStartIndex + i]
														.length -
														errorRate.wordLevel.reference[alignment.referenceStartIndex + i].length,
													0
												)
											) +
											errorRate.wordLevel.reference[alignment.referenceStartIndex + i]}
									{/each}
								</span>
							{/if}
							<span> </span>
						{/each}
					</h4>
					<h4 class="whitespace-nowrap">
						{#each errorRate.wordLevel.alignments as alignment}
							{#if alignment.type === 'equal'}
								<span class="bg-lime-400">
									{errorRate.wordLevel.hypothesis
										.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
										.reduce((acc, cur) => acc + ' ' + cur, '')}
								</span>
							{:else if alignment.type === 'insert'}
								<span class="bg-sky-400">
									{errorRate.wordLevel.hypothesis
										.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
										.reduce((acc, cur) => acc + ' ' + cur, '')}
								</span>
							{:else if alignment.type === 'delete'}
								<span class="bg-red-600">
									{errorRate.wordLevel.reference
										.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
										.reduce((acc, cur) => acc + ' ' + cur, '')
										.replaceAll(/\S/g, '_')}
								</span>
							{:else if alignment.type === 'substitute'}
								<span class="bg-amber-500">
									{#each getNumberArray(alignment.hypothesisEndIndex - alignment.hypothesisStartIndex) as i}
										{' ' +
											'_'.repeat(
												Math.max(
													errorRate.wordLevel.reference[alignment.referenceStartIndex + i].length -
														errorRate.wordLevel.hypothesis[alignment.hypothesisStartIndex + i]
															.length,
													0
												)
											) +
											errorRate.wordLevel.hypothesis[alignment.hypothesisStartIndex + i]}
									{/each}
								</span>
							{/if}
							<span> </span>
						{/each}
					</h4>
				</div>

				<h3>cer: {(errorRate.characterLevel.cer * 100).toFixed(2) + '%'}</h3>
				<div class="flex-1">
					<span>hits: {errorRate.characterLevel.hits}</span>
					<span>substitutions: {errorRate.characterLevel.substitutions}</span>
					<span>deletions: {errorRate.characterLevel.deletions}</span>
				</div>
				<div class="border-box overflow-x-auto font-mono">
					<h4 class="whitespace-nowrap">
						{#each errorRate.characterLevel.alignments as alignment}
							{#if alignment.type === 'equal'}
								<span class="bg-lime-400">
									{errorRate.characterLevel.reference
										.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
										.reduce((acc, cur) => acc + cur, '')}
								</span>
							{:else if alignment.type === 'delete'}
								<span class="bg-red-600">
									{errorRate.characterLevel.reference
										.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
										.reduce((acc, cur) => acc + cur, '')}
								</span>
							{:else if alignment.type === 'insert'}
								<span class="bg-sky-400">
									{errorRate.characterLevel.hypothesis
										.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
										.reduce((acc, cur) => acc + cur, '')
										.replaceAll(/\S/g, '_')}
								</span>
							{:else if alignment.type === 'substitute'}
								<span class="bg-amber-500">
									{#each getNumberArray(alignment.hypothesisEndIndex - alignment.hypothesisStartIndex) as i}
										{'_'.repeat(
											Math.max(
												errorRate.characterLevel.hypothesis[alignment.hypothesisStartIndex + i]
													.length -
													errorRate.characterLevel.reference[alignment.referenceStartIndex + i]
														.length,
												0
											)
										) + errorRate.characterLevel.reference[alignment.referenceStartIndex + i]}
									{/each}
								</span>
							{/if}
						{/each}
					</h4>
					<h4 class="whitespace-nowrap">
						{#each errorRate.characterLevel.alignments as alignment}
							{#if alignment.type === 'equal'}
								<span class="bg-lime-400">
									{errorRate.characterLevel.hypothesis
										.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
										.reduce((acc, cur) => acc + cur, '')}
								</span>
							{:else if alignment.type === 'insert'}
								<span class="bg-sky-400">
									{errorRate.characterLevel.hypothesis
										.slice(alignment.hypothesisStartIndex, alignment.hypothesisEndIndex)
										.reduce((acc, cur) => acc + cur, '')}
								</span>
							{:else if alignment.type === 'delete'}
								<span class="bg-red-600">
									{errorRate.characterLevel.reference
										.slice(alignment.referenceStartIndex, alignment.referenceEndIndex)
										.reduce((acc, cur) => acc + cur, '')
										.replaceAll(/\S/g, '_')}
								</span>
							{:else if alignment.type === 'substitute'}
								<span class="bg-amber-500">
									{#each getNumberArray(alignment.hypothesisEndIndex - alignment.hypothesisStartIndex) as i}
										{'_'.repeat(
											Math.max(
												errorRate.characterLevel.reference[alignment.referenceStartIndex + i]
													.length -
													errorRate.characterLevel.hypothesis[alignment.hypothesisStartIndex + i]
														.length,
												0
											)
										) + errorRate.characterLevel.hypothesis[alignment.hypothesisStartIndex + i]}
									{/each}
								</span>
							{/if}
						{/each}
					</h4>
				</div>
			{/each}
		</div>
	{:else}
		<h2>This file has no ground truth</h2>
	{/if}
</div>
