import { TaskKanban } from '../components/TaskKanban'
import { Modal, Card } from '@mui/material'
import { useState } from 'react'
import { TaskForm } from '../components/TaskForm'

export function HomePage() {
  const [modalOpen, setModalOpen] = useState(false)
  const [taskRefreshTrigger, setTaskRefreshTrigger] = useState(0)

  function handleNewTaskButtonClick() {
    setModalOpen(true)
  }

  function handleModalClose() {
    setModalOpen(false)
  }

  function handleNewTaskCreated() {
    setModalOpen(false)
    setTaskRefreshTrigger((trigger) => trigger + 1)
  }

  return (
    <>
      <TaskKanban
        handleNewTaskButtonClick={handleNewTaskButtonClick}
        refreshTrigger={taskRefreshTrigger}
      />
      <Modal open={modalOpen} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Card>
          <TaskForm
            mode="create"
            onSaved={handleNewTaskCreated}
            onCancel={handleModalClose}
          />
        </Card>
      </Modal>
    </>
  )
}
