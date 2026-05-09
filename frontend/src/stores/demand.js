import { defineStore } from 'pinia'
import { demandAPI, matchAPI } from '../api'

export const useDemandStore = defineStore('demand', {
  state: () => ({
    demands: [],
    currentDemand: null,
    matchResult: null,
    matchStatus: null
  }),
  actions: {
    async fetchList() {
      const res = await demandAPI.list()
      this.demands = res.data
    },
    async fetchDetail(id) {
      const res = await demandAPI.detail(id)
      this.currentDemand = res.data
    },
    async create(data) {
      return await demandAPI.create(data)
    },
    async runMatch(demandId) {
      await matchAPI.run(demandId)
      this.matchStatus = 'pending'
    },
    async pollResult(demandId) {
      const res = await matchAPI.result(demandId)
      this.matchStatus = res.data.status
      if (res.data.status === 'done') {
        this.matchResult = res.data.result
      }
      return res.data
    }
  }
})
