import used from '$lib/utils';
import type {
	DockviewApi,
	DockviewGroupPanel,
	GroupPanelPartInitParameters,
	IContentRenderer,
	IGroupHeaderProps,
	IHeaderActionsRenderer,
	ITabRenderer,
	PanelUpdateEvent,
	Parameters
} from 'dockview-core';

import { type SvelteComponent, mount, unmount, type ComponentType } from 'svelte';

abstract class AbstractSvelteRenderer<S extends Record<string, unknown>> {
	readonly _element: HTMLElement;
	readonly _component: ComponentType<SvelteComponent<S>>;
	protected _instance: ComponentType<SvelteComponent<S>> | undefined;

	get element() {
		return this._element;
	}

	get component() {
		return this._component;
	}

	constructor(component: ComponentType<SvelteComponent<S>>) {
		this._component = component;

		this._element = document.createElement('div');
		this.element.className = 'dv-vue-part';
		this.element.style.height = '100%';
	}
}

export class SvelteRenderer<S extends Record<string, unknown>>
	extends AbstractSvelteRenderer<S>
	implements IContentRenderer, ITabRenderer
{
	private _props: S | undefined;

	constructor(component: ComponentType<SvelteComponent<S>>) {
		super(component);
	}

	init(parameters: GroupPanelPartInitParameters): void {
		this._props = parameters.params as S;

		this._instance = mount(this._component, {
			target: this._element,
			props: this._props
		}) as ComponentType<SvelteComponent<S>>;
	}

	update(event: PanelUpdateEvent<Parameters>): void {
		if (this._instance === undefined) {
			return;
		}

		const params = event.params.params as S;
		this._props = { ...(this._props as S), ...params };
	}

	dispose(): void {
		if (this._instance !== undefined) {
			unmount(this._instance);
		}
	}
}

type TabRequirements<S = Record<string, unknown>> = {
	containerApi: DockviewApi;
	defaultProps: S;
};

export class SvelteTabActionRenderer<P extends Record<string, unknown>>
	extends AbstractSvelteRenderer<TabRequirements<P>>
	implements IHeaderActionsRenderer
{
	private _defaultProps: P;

	constructor(
		component: ComponentType<SvelteComponent<TabRequirements<P>>>,
		group: DockviewGroupPanel,
		defaultProps: P
	) {
		super(component);
		used(group);
		this._defaultProps = defaultProps;
	}

	init(params: IGroupHeaderProps): void {
		const props: TabRequirements<P> = {
			...params,
			defaultProps: this._defaultProps
		};

		this._instance = mount(this._component, {
			target: this._element,
			props
		}) as ComponentType<SvelteComponent<TabRequirements<P>>>;
	}

	dispose(): void {
		if (this._instance !== undefined) {
			unmount(this._instance);
		}
	}
}
