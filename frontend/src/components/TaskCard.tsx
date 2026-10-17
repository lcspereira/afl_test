import Box from '@mui/material/Box'
import Card from '@mui/material/Card'
import CardContent from '@mui/material/CardContent'
import IconButton from '@mui/material/IconButton'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import Typography from '@mui/material/Typography'
import MoreVertIcon from '@mui/icons-material/MoreVert'
import { useState } from 'react'
import type { Task } from '../services/taskService'

interface TaskCardProps {
  task: Task
  isSaving: boolean
  isDragging: boolean
  onDragStart: (taskId: number) => void
  onDragEnd: () => void
  onEdit: (task: Task) => void
  onDelete: (task: Task) => void
}

export function TaskCard({
  task,
  isSaving,
  isDragging,
  onDragStart,
  onDragEnd,
  onEdit,
  onDelete,
}: TaskCardProps) {
  const [menuAnchor, setMenuAnchor] = useState<HTMLElement | null>(null)

  function closeMenu() {
    setMenuAnchor(null)
  }

  return (
    <Card
      draggable={task.id !== undefined && !isSaving}
      onDragStart={(event) => {
        if (task.id === undefined) {
          event.preventDefault()
          return
        }

        event.dataTransfer.setData('text/plain', String(task.id))
        event.dataTransfer.effectAllowed = 'move'
        onDragStart(task.id)
      }}
      onDragEnd={onDragEnd}
      sx={{
        cursor: isSaving ? 'wait' : 'grab',
        opacity: isDragging ? 0.5 : 1,
      }}
    >
      <CardContent>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            gap: 1,
          }}
        >
          <Typography variant="subtitle1" component="h3">
            {task.titulo}
          </Typography>
          <IconButton
            aria-label={`Ações para ${task.titulo}`}
            aria-haspopup="menu"
            disabled={task.id === undefined || isSaving}
            onClick={(event) => {
              event.stopPropagation()
              setMenuAnchor(event.currentTarget)
            }}
            onMouseDown={(event) => event.stopPropagation()}
            size="small"
          >
            <MoreVertIcon />
          </IconButton>
        </Box>
        <Typography
          variant="body2"
          color="text.secondary"
          sx={{
            mt: 1,
            overflowWrap: 'anywhere',
            whiteSpace: 'pre-wrap',
          }}
        >
          {task.descricao}
        </Typography>
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ display: 'block', mt: 2 }}
        >
          Criada em{' '}
          {task.data_criacao
            ? new Date(task.data_criacao).toLocaleDateString()
            : 'N/A'}
        </Typography>
      </CardContent>
      <Menu
        anchorEl={menuAnchor}
        open={Boolean(menuAnchor)}
        onClose={closeMenu}
      >
        <MenuItem
          onClick={() => {
            closeMenu()
            onEdit(task)
          }}
        >
          Editar
        </MenuItem>
        <MenuItem
          onClick={() => {
            closeMenu()
            onDelete(task)
          }}
        >
          Excluir
        </MenuItem>
      </Menu>
    </Card>
  )
}
