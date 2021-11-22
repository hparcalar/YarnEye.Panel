import { ColorAssignment, ProdLine } from '../models/yarn.models';
import { ApiGeneric } from './base/api.generic';

export class YarnEyeService {
  apiObject: ApiGeneric = new ApiGeneric();

  // #region PROD LINES
  async getProdLineList() {
    const data = await this.apiObject.getAll('ProdLine');
    return data;
  }

  async getProdLine(id: number) {
    const data = await this.apiObject.get('ProdLine', id);
    return data;
  }

  async saveProdLine(model: ProdLine) {
      return await this.apiObject.save('ProdLine', model);
  }
  // #endregion

  // #region ASSIGNMENTS
  async getAssignmentList() {
    const data = await this.apiObject.getAll('ColorAssignment');
    return data;
  }

  async getAssignment(id: number) {
    const data = await this.apiObject.get('ColorAssignment', id);
    return data;
  }

  async saveAssignment(model: ColorAssignment) {
      return await this.apiObject.save('ColorAssignment', model);
  }
  // #endregion

  // #region PYTHON CALLS
  async openAssignment(lineList: string) {
    return await this.apiObject.save('ActiveAssigner', {
      selectedLines: lineList,
      ipAddr: '127.0.1.1',
      assignerStatus: 1,
    })
  }

  async openTester(prodLineId: number) {
    return await this.apiObject.save('ActiveTester', {
      ipAddr: '127.0.1.1',
      prodLineId: prodLineId,
      testerStatus: 1,
    })
  }
  // #endregion
}
