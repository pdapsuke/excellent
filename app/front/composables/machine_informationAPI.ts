// マシン情報作成時のリクエストボディの型定義
interface MachineInformationPost {
    ballspeed: string[]
    pitch_type: string[]
    batter_box: string
    username: string
    place_id: string
}


// useBattingCenterApiの名前で関数をエクスポート
export const useMachineInformationApi = () => {
    return {
      // マシン情報の投稿
      async post(machine_information: MachineInformationPost) {
        return useApi().post<any>("postMachineInformation", "/machine_informations/", machine_information)
      },
      // マシン情報毎のあった！なかった！数を取得
      async get(machine_id: number, atta_nakatta: string) {
        return useApi().get<any>("getAttaCount", `/machine_informations/${machine_id}/atta_nakatta`, {"atta_nakatta": atta_nakatta})
      },
    }
}