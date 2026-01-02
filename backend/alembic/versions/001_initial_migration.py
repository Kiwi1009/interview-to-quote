"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('pm', 'sales', 'integrator', 'admin', name='userrole'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Cases table
    op.create_table(
        'cases',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('industry', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('draft', 'extracting', 'reviewing', 'quoted', 'archived', name='casestatus'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cases_id'), 'cases', ['id'], unique=False)

    # Uploads table
    op.create_table(
        'uploads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('transcript', 'photo', name='uploadtype'), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('sha256', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_uploads_id'), 'uploads', ['id'], unique=False)
    op.create_index(op.f('ix_uploads_sha256'), 'uploads', ['sha256'], unique=True)

    # Transcript segments table
    op.create_table(
        'transcript_segments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('idx', sa.Integer(), nullable=False),
        sa.Column('speaker', sa.String(), nullable=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('start_char', sa.Integer(), nullable=False),
        sa.Column('end_char', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transcript_segments_id'), 'transcript_segments', ['id'], unique=False)

    # Extraction runs table
    op.create_table(
        'extraction_runs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=True),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('prompt_hash', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'running', 'completed', 'failed', name='extractionstatus'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('finished_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extraction_runs_id'), 'extraction_runs', ['id'], unique=False)

    # Extracted requirements table
    op.create_table(
        'extracted_requirements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.Integer(), nullable=False),
        sa.Column('jsonb_data', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('confidence', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['run_id'], ['extraction_runs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_extracted_requirements_id'), 'extracted_requirements', ['id'], unique=False)

    # Evidence table
    op.create_table(
        'evidence',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.Integer(), nullable=False),
        sa.Column('field_path', sa.String(), nullable=False),
        sa.Column('segment_idx', sa.Integer(), nullable=True),
        sa.Column('snippet', sa.String(), nullable=False),
        sa.Column('start_char', sa.Integer(), nullable=True),
        sa.Column('end_char', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['run_id'], ['extraction_runs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_evidence_id'), 'evidence', ['id'], unique=False)

    # Plans table
    op.create_table(
        'plans',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.Integer(), nullable=True),
        sa.Column('plan_code', sa.Enum('P1', 'P2', 'P3', name='plancode'), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('assumptions_jsonb', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.ForeignKeyConstraint(['run_id'], ['extraction_runs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plans_id'), 'plans', ['id'], unique=False)

    # Quote items table
    op.create_table(
        'quote_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plan_id', sa.Integer(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('item_name', sa.String(), nullable=False),
        sa.Column('spec', sa.String(), nullable=True),
        sa.Column('qty', sa.Float(), nullable=True),
        sa.Column('unit', sa.String(), nullable=True),
        sa.Column('unit_price_low', sa.Float(), nullable=False),
        sa.Column('unit_price_high', sa.Float(), nullable=False),
        sa.Column('subtotal_low', sa.Float(), nullable=True),
        sa.Column('subtotal_high', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_quote_items_id'), 'quote_items', ['id'], unique=False)

    # Documents table
    op.create_table(
        'documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('case_id', sa.Integer(), nullable=False),
        sa.Column('run_id', sa.Integer(), nullable=True),
        sa.Column('doc_type', sa.Enum('spec', 'report', 'quote', name='documenttype'), nullable=False),
        sa.Column('format', sa.Enum('docx', 'pdf', name='documentformat'), nullable=False),
        sa.Column('path', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['case_id'], ['cases.id'], ),
        sa.ForeignKeyConstraint(['run_id'], ['extraction_runs.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')
    op.drop_index(op.f('ix_quote_items_id'), table_name='quote_items')
    op.drop_table('quote_items')
    op.drop_index(op.f('ix_plans_id'), table_name='plans')
    op.drop_table('plans')
    op.drop_index(op.f('ix_evidence_id'), table_name='evidence')
    op.drop_table('evidence')
    op.drop_index(op.f('ix_extracted_requirements_id'), table_name='extracted_requirements')
    op.drop_table('extracted_requirements')
    op.drop_index(op.f('ix_extraction_runs_id'), table_name='extraction_runs')
    op.drop_table('extraction_runs')
    op.drop_index(op.f('ix_transcript_segments_id'), table_name='transcript_segments')
    op.drop_table('transcript_segments')
    op.drop_index(op.f('ix_uploads_sha256'), table_name='uploads')
    op.drop_index(op.f('ix_uploads_id'), table_name='uploads')
    op.drop_table('uploads')
    op.drop_index(op.f('ix_cases_id'), table_name='cases')
    op.drop_table('cases')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

