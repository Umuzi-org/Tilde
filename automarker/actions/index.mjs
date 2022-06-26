export class Action {
  async execute({ test, ...params }) {
    let result = null;
    if (test && this.testAction) {
      result = this.testAction({ ...params });
    } else {
      result = this.action({ ...params });
    }
    result = await result;
    return result;
  }
}
