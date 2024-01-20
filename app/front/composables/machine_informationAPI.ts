// マシン情報作成時のリクエストボディの型定義
interface MachineInformationPost {
    ballspeed_ids: number[]
    breaking_ball_ids: number[]
    batter_box: string
}

interface BreakingBall {
  id: number
  name: string
}

interface BallSpeed {
  id: number
  speed: number
}

interface MachineInformation{
  id: number
  user_id: number
  breaking_balls: BreakingBall[]
  ball_speeds: BallSpeed[]
  atta_count: number
  atta: string
  nakatta_count: number
  nakatta: string
  updated: string
}

// useBattingCenterApiの名前で関数をエクスポート
export const useMachineInformationApi = () => {
  return {
    // マシン情報の投稿
    async postMachineInformation(battingCenterId: number, machineInformation: MachineInformationPost) {
      return useApi().post<any>("postMachineInformation", `/batting_centers/${battingCenterId}/machine_informations`, machineInformation)
    },
    // バッティングセンターごとのマシン情報一覧取得
    async getMachineInformation(battingCenterId: number) {
      return useApi().get<MachineInformation>("getMachineInformations", `/batting_centers/${battingCenterId}/machine_informations`)
    },
    // マシン情報毎のあった！なかった！数を取得
    async get(machine_id: number, atta_nakatta: string) {
      return useApi().get<any>("getAttaCount", `/machine_informations/${machine_id}/atta_nakatta`, {"atta_nakatta": atta_nakatta})
    },
    // 球速一覧の取得
    async getBallSpeeds() {
      return useApi().get<BallSpeed>("getBallSpeeds", "/machine_configurations/ball_speeds")
    },
    // 球種一覧の取得
    async getBreakingBalls() {
      return useApi().get<BreakingBall>("getBreakingBalls", "/machine_configurations/breaking_balls")
    },
  }
}