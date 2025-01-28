"""
@Author = 'Michael Stanley'

============ Change Log ============
2025-Jan-03 = Created. 

============ License ============
Copyright (C) 2025 Michael Stanley

This file is part of wmul_rivendell.

wmul_rivendell is free software: you can redistribute it and/or modify it 
under the terms of the GNU General Public License as published by the Free 
Software Foundation, either version 3 of the License, or (at your option) any 
later version.

wmul_rivendell is distributed in the hope that it will be useful, but WITHOUT 
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
wmul_rivendell. If not, see <https://www.gnu.org/licenses/>. 
"""
import pytest
from pathlib import Path

from wmul_rivendell.LoadCartDataDump import RivendellCart, CartType
from wmul_rivendell.DatabaseStatistics import DatabaseStatistics, StatisticsLimits

from wmul_test_utils import generate_true_false_matrix_from_list_of_strings

def test__organize_by_rivendell_group():
    defined_carts = [
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='facilis porro numquam nulla', artist='nostrum illum', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='illo deserunt inventore accusamus', artist='a quas', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='nihil ratione optio saepe', artist='quisquam fugit', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='praesentium nihil aperiam deleniti', artist='similique at', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='sapiente laboriosam aliquam impedit', artist='harum dolores', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='commodi voluptatibus nisi officia', artist='odit facere', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='occaecati dolorum eius molestias', artist='atque provident', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='odio quasi recusandae inventore', artist='autem at', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='accusamus consequatur quis quisquam', artist='quo ex', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='LAUDANTIUM', title='modi dolores aliquam aut', artist='exercitationem deserunt', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='reiciendis dolore consectetur harum', artist='dolore temporibus', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='labore commodi voluptatum nam', artist='perferendis perspiciatis', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='dolore quidem nulla culpa', artist='quas facilis', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='impedit rerum debitis magni', artist='deserunt vitae', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='rem id cupiditate culpa', artist='cum aliquid', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='dolor aliquam deserunt laboriosam', artist='ipsa dicta', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='blanditiis illum cupiditate tempora', artist='labore voluptatum', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='assumenda blanditiis natus incidunt', artist='error quibusdam', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='vero a eius ab', artist='aut quae', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='ASPERIORES', title='labore explicabo voluptas nisi', artist='dignissimos veritatis', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='magnam sed repellat iusto', artist='libero beatae', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='laborum laborum ipsum corrupti', artist='voluptatum nisi', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='alias dolorum qui odit', artist='recusandae perspiciatis', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='reiciendis architecto cupiditate aperiam', artist='optio nesciunt', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='omnis voluptas voluptates molestias', artist='similique natus', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='molestias non laborum eligendi', artist='eaque aliquid', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='placeat similique eligendi nobis', artist='expedita est', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='quasi consectetur sequi ab', artist='saepe cumque', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='natus doloremque earum repellendus', artist='deserunt corporis', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='assumenda aliquam itaque doloremque', artist='placeat ipsa', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='iure ad consequatur similique', artist='necessitatibus iusto', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='consectetur ad provident iusto', artist='cumque error', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='quod praesentium odit animi', artist='accusamus dolorum', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='in ex tempora aspernatur', artist='laborum tempora', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='facilis itaque dolore tenetur', artist='earum occaecati', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='reprehenderit alias hic necessitatibus', artist='maxime fugiat', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='modi recusandae atque provident', artist='necessitatibus consequatur', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='delectus itaque rerum recusandae', artist='minima neque', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='voluptates sint nihil magnam', artist='perspiciatis dolorem', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='EXPLICABO', title='sed voluptas porro beatae', artist='architecto a', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='iure voluptatibus magnam sed', artist='dolor vel', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='nobis accusamus minus beatae', artist='dicta hic', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='2004', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='quam odio iure doloribus', artist='nam excepturi', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='2004', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='at in nisi excepturi', artist='adipisci facere', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='enim alias repellat tempora', artist='consectetur doloribus', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='2013', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='reiciendis architecto animi molestias', artist='consequatur magnam', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='2015', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='deserunt debitis distinctio totam', artist='unde aliquid', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='cum autem perferendis eveniet', artist='dolores occaecati', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='nihil dolore sint dicta', artist='quasi voluptates', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='quos doloremque distinctio laudantium', artist='sed aut', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='architecto debitis eos deserunt', artist='aspernatur molestiae', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='perferendis aliquam alias corrupti', artist='quam exercitationem', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='quas aut vitae ipsum', artist='suscipit repudiandae', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='deserunt veniam voluptas ab', artist='eligendi cum', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='at nobis placeat cum', artist='distinctio sequi', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='doloribus expedita est aut', artist='commodi illum', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='impedit tempora reiciendis dolorum', artist='minus eum', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='nemo consequatur fugiat impedit', artist='corporis commodi', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='cumque distinctio suscipit dolorem', artist='maiores quia', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes=''),
        RivendellCart(cart_number='', cut_number='1', type=CartType.Audio, group_name='POSSIMUS', title='aspernatur ipsa ex atque', artist='cupiditate eveniet', album='', year='', isrc='', isci='', label='', client='', agency='', publisher='', composer='', conductor='', song_id='', user_defined='', description='', outcue='', filename='', length='', start_point='', end_point='', segue_start_point='', segue_end_point='', hook_start_point='', hook_end_point='', talk_start_point='', talk_end_point='', fadeup_point='', fadedown_point='', sched_codes='')
    ]

    mock_rivendell_carts = "mock_rivendell_carts"
    mock_filename = "mock_filename"

    stats_limits = StatisticsLimits()

    ds = DatabaseStatistics(
        rivendell_carts=mock_rivendell_carts, 
        output_filename=mock_filename, 
        stats_limits=stats_limits,
        write_limits=False
    )

    organized_carts = ds._organize_by_rivendell_group(defined_carts)

    assert len(organized_carts.keys()) == 4
    
    LAUDANTIUM_carts = organized_carts["LAUDANTIUM"]
    assert len(LAUDANTIUM_carts) == 10

    ASPERIORES_carts = organized_carts["ASPERIORES"]
    assert len(ASPERIORES_carts) == 10

    EXPLICABO_carts = organized_carts["EXPLICABO"]
    assert len(EXPLICABO_carts) == 20

    POSSIMUS_carts = organized_carts["POSSIMUS"]
    assert len(POSSIMUS_carts) == 20




write_csv_params, write_csv_ids = \
    generate_true_false_matrix_from_list_of_strings(
        "write_csv",
        [
            "write_limits"
        ]

    )

@pytest.mark.parametrize("params", write_csv_params, ids=write_csv_ids)
def test__write_csv(fs, mocker, params):
    import pandas as pd
    laudantium_line = pd.Series({
        "Group Name2": "laudantium", 
        "Number of Songs": "mock",
        "Shortest Song Length": "line"
    })
    laudantium_mock = mocker.Mock(
        to_pandas_series=mocker.Mock(return_value=laudantium_line)
    )

    asperiores_line = pd.Series({
        "Group Name2": "asperiores", 
        "Number of Songs": "abcd",
        "Shortest Song Length": "efgh"
    })
    asperiores_mock = mocker.Mock(
        to_pandas_series=mocker.Mock(return_value=asperiores_line)
    )

    explicabo_line = pd.Series({
        "Group Name2": "explicabo", 
        "Number of Songs": "jklm",
        "Shortest Song Length": "nopq"
    })
    explicabo_mock = mocker.Mock(
        to_pandas_series=mocker.Mock(return_value=explicabo_line)
    )

    possimus_line = pd.Series({
        "Group Name2": "possimus", 
        "Number of Songs": "rstu",
        "Shortest Song Length": "vwxy"
    })
    possimus_mock = mocker.Mock(
        to_pandas_series=mocker.Mock(return_value=possimus_line)
    )

    statistics_per_group = {
        "LAUDANTIUM": laudantium_mock,
        "ASPERIORES": asperiores_mock,
        "EXPLICABO": explicabo_mock,
        "POSSIMUS": possimus_mock
    }

    data_contents = "Group Name,Group Name2,Number of Songs,Shortest Song Length\n" \
        "ASPERIORES,asperiores,abcd,efgh\n" \
        "EXPLICABO,explicabo,jklm,nopq\n" \
        "LAUDANTIUM,laudantium,mock,line\n" \
        "POSSIMUS,possimus,rstu,vwxy\n"
        

    if params.write_limits:
        expected_file_contents = ",Smallest Standard Deviation,Minimum Population for Outliers,Lower Bound Multiple," \
            "Upper Bound Multiple\nStatistics Limits,0:00:15,4,1.5,3.0\n" + data_contents
    else:
        expected_file_contents = data_contents


    root_dir = Path(r"test")
    root_dir.mkdir()

    pathname = root_dir / 'testfile.csv'

    mock_rivendell_carts = "mock_rivendell_carts"

    stats_limits = StatisticsLimits()
    ds = DatabaseStatistics(
        rivendell_carts=mock_rivendell_carts, 
        output_filename=pathname, 
        stats_limits=stats_limits,
        write_limits=params.write_limits
    )

    ds._write_csv(statistics_per_group=statistics_per_group)

    assert pathname.read_text() == expected_file_contents

