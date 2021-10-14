export interface ProdLine{
    prodLineId: number
    prodLineCode: string
    prodLineName: string
    orderNo: number | null
    assignmentId: number | null
}

export interface ColorAssignment {
    assignmentId: number
    assignmentCode: string
    sampleImage: any
    setHue: number | null
    setSaturation: number | null
    setValue: number | null
    isActive: boolean
    createdDate: string
}