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
  is_owner: boolean
  breaking_balls: BreakingBall[]
  ball_speeds: BallSpeed[]
  atta_count: number
  atta: string
  nakatta_count: number
  nakatta: string
  updated: string
}

interface BattingCenterAndMachines {
  id: number
  place_id: string
  name: string
  formatted_address: string
  machine_informations: MachineInformation[]
}

interface AttaNakattaUpdateResponse {
	id: number
	atta_count: number
	nakatta_count: number
	atta: string
	nakatta: string
}

export const useUtil = () => {
  return {
		// 日付をYYYY/MM/DD形式に変換
		formatDate(datetime: string): string {
			let d = new Date(datetime) 
			let year = d.getFullYear()
			let month = d.getMonth() + 1
			let day = d.getDate()
			return `${year}/${month}/${day}`    
		},
		// マシン情報編集コンポーネントに選択済みの球速一覧を渡すための処理
		createSelectedBallSpeedsList(machineInformation: MachineInformation) {
			return machineInformation.ball_speeds.map((x) => x.id)
		},
		// マシン情報編集コンポーネントに選択済みの球種一覧を渡すための処理
		createSelectedBreakingBallsList(machineInformation: MachineInformation) {
			return machineInformation.breaking_balls.map((x) => x.id)
		},
		// MachineInformation型オブジェクトのあった！なかった！フラグを更新
		updateAttaNakattaForMachineInformation(machineInformations: MachineInformation[], machineInformation: MachineInformation,attaNakattaUpdateResponse: AttaNakattaUpdateResponse) {
			machineInformations.filter((x) => x.id == machineInformation.id)[0].atta = attaNakattaUpdateResponse.atta
			machineInformations.filter((x) => x.id == machineInformation.id)[0].atta_count = attaNakattaUpdateResponse.atta_count
			machineInformations.filter((x) => x.id == machineInformation.id)[0].nakatta = attaNakattaUpdateResponse.nakatta
			machineInformations.filter((x) => x.id == machineInformation.id)[0].nakatta_count = attaNakattaUpdateResponse.nakatta_count				
		},
		// BattingCenterAndMachinesオブジェクトのあった！なかった！フラグを更新
		updateAttaNakattaForBattingCenterAndMachines(battingCenterId: number, battingCenterAndMachines: BattingCenterAndMachines[], machineInformation: MachineInformation, attaNakattaUpdateResponse: AttaNakattaUpdateResponse) {
			battingCenterAndMachines.filter((x) => x.id == battingCenterId)[0].machine_informations.filter((x) => x.id == machineInformation.id)[0].atta = attaNakattaUpdateResponse.atta
			battingCenterAndMachines.filter((x) => x.id == battingCenterId)[0].machine_informations.filter((x) => x.id == machineInformation.id)[0].atta_count = attaNakattaUpdateResponse.atta_count
			battingCenterAndMachines.filter((x) => x.id == battingCenterId)[0].machine_informations.filter((x) => x.id == machineInformation.id)[0].nakatta = attaNakattaUpdateResponse.nakatta
			battingCenterAndMachines.filter((x) => x.id == battingCenterId)[0].machine_informations.filter((x) => x.id == machineInformation.id)[0].nakatta_count = attaNakattaUpdateResponse.nakatta_count
		},
	}
}
